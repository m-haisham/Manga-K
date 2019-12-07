class DictClass:
    def todict(self):
        return vars(self)

    def fromdict(self, obj):
        if obj is None:
            return self

        try:
            instance_keys = list(vars(self).keys())

            for key in obj.keys():
                if key in instance_keys:
                    setattr(self, key, obj[key])

            return self
        except KeyError as e:
            print(e)
            return self

