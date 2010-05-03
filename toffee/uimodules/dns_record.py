from toffee.uimodules import UIModule

class ARecords(UIModule):

    def render(self, records):
        return self.render_string("modules/a_record.html", records=records)

ARecords.register()
