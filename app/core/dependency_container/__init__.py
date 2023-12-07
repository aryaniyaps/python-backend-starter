import asyncio
from typing import Callable, Type, TypeVar, Union

T = TypeVar("T")


class DependencyContainer:
    def __init__(self) -> None:
        self.dependencies = {}

    def register(
        self,
        key: Type[T],
        dependency: Union[T, Callable[[], T], Callable[[], asyncio.Task[T]]],
    ):
        """
        Register a dependency with a given key.
        :param key: The key (class) to identify the dependency.
        :param dependency: The actual dependency object, a factory callable, or an async factory callable.
        """
        self.dependencies[key] = dependency

    def resolve(self, key: Type[T]) -> T:
        """
        Resolve a dependency by its key.
        :param key: The key (class) of the dependency to resolve.
        :return: The resolved dependency.
        :raises KeyError: If the key is not found in the container.
        """
        if key not in self.dependencies:
            raise KeyError(f"Dependency with key '{key}' not found.")

        dependency = self.dependencies[key]

        if asyncio.iscoroutinefunction(dependency):
            # If the dependency is an async factory, await it
            return asyncio.run(dependency())

        if callable(dependency):
            # If the dependency is a callable, assume it's a factory and call it
            return dependency()

        return dependency
