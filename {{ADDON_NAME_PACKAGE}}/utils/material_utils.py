class MaterialUtils:

    @staticmethod
    def has_materials(obj):
        for slot in obj.material_slots:
            if slot.material:
                return True
        return False