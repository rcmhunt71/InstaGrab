from instagrab.config.config_const import ConfigConstants as CfgConsts


# TODO: Document (docstring and inlines) + typing + class level

class UiUtils:

    @staticmethod
    def get_dimensions(cfg, path):
        width_path = path.copy()
        width_path.append(CfgConsts.WIDTH)
        height_path = path.copy()
        height_path.append(CfgConsts.HEIGHT)

        width = cfg.get_element(path=width_path, default=200)
        height = cfg.get_element(path=height_path, default=200)
        return width, height
