class UiUtils:

    @staticmethod
    def update_ui(context):
        for region in context.area.regions:
            if region.type == "UI":
                region.tag_redraw()
