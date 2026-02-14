import inspect
from typing import Type, TypeVar, Dict, Callable, Any, Optional
from dataclasses import dataclass


T = TypeVar('T')


@dataclass
class ServiceDescriptor:
    service_type: Type
    implementation: Type | Callable
    lifetime: str = "singleton"


class DIContainer:
    def __init__(self):
        self._services: Dict[Type, ServiceDescriptor] = {}
        self._singletons: Dict[Type, Any] = {}

    def register(
        self,
        service_type: Type[T],
        implementation: Optional[Type[T] | Callable[[], T]] = None,
        lifetime: str = "singleton"
    ):
        if implementation is None:
            implementation = service_type
        self._services[service_type] = ServiceDescriptor(
            service_type=service_type,
            implementation=implementation,
            lifetime=lifetime
        )

    def register_instance(self, service_type: Type[T], instance: T):
        self._singletons[service_type] = instance

    def resolve(self, service_type: Type[T]) -> T:
        descriptor = self._services.get(service_type)
        if not descriptor:
            raise KeyError(f"Service {service_type} not registered")

        if descriptor.lifetime == "singleton":
            if service_type not in self._singletons:
                self._singletons[service_type] = self._create_instance(descriptor)
            return self._singletons[service_type]

        return self._create_instance(descriptor)

    def _create_instance(self, descriptor: ServiceDescriptor) -> Any:
        implementation = descriptor.implementation
        sig = inspect.signature(implementation.__init__)
        params = {}

        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            if param.annotation != inspect.Parameter.empty:
                try:
                    params[param_name] = self.resolve(param.annotation)
                except KeyError:
                    if param.default != inspect.Parameter.empty:
                        continue
                    raise

        return implementation(**params)


container = DIContainer()
