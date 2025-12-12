class ConstMeta(type):    
    def __setattr__(cls, name, value):
        const = {"FONT", "FONT_STYLE1", "H2_STYLE", "COLOUR1", "COLOUR2", "COLOUR3", "COLOUR4", "COLOUR5"}
        if name in const:
            raise AttributeError(f"Cannot modify constant: '{name}'")
        super().__setattr__(name, value)