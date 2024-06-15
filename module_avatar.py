from gdo.base.GDO_Module import GDO_Module


class module_avatar(GDO_Module):

    def gdo_dependencies(self) -> list:
        return [
            'file',
        ]
    