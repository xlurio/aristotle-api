from rest_framework import routers


class WriteOnlyRouter(routers.SimpleRouter):
    """Router for write only end points"""

    routes = [
        routers.Route(
            url=r"^{prefix}$",
            mapping={"post": "create"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
    ]


class ReadOnlyRouter(routers.SimpleRouter):
    """Router for read only end points"""

    routes = [
        routers.Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={
                "get": "list",
            },
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        routers.Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={
                "get": "retrieve",
            },
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
    ]
