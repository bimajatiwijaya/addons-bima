odoo.define('pos_password_protected.pos_custom', function(require){
    "use strict";
//    var gui = require('point_of_sale.gui');
//    var popup = require('point_of_sale.popups');
    var screens = require('point_of_sale.screens');
//    gui.define_popup({name:'check_user', widget: ConfirmUserPasswordPopupWidget});
//    var _super_numpad_widget = screens.NumpadWidget.prototype;
    var ConfirmWidget = screens.NumpadWidget.extend({
        template: 'NumpadWidget',
        clickChangeMode: function(event) {
            var newMode = event.currentTarget.attributes['data-mode'].nodeValue;
            console.log("==========");
            return this.state.changeMode(newMode);
        },
        changedMode: function() {
            var mode = this.state.get('mode');
            console.log("SSSSSSSSSSSSSSSSS");
            $('.selected-mode').removeClass('selected-mode');
            $(_.str.sprintf('.mode-button[data-mode="%s"]', mode), this.$el).addClass('selected-mode');
        },
//        renderElement: function(){
//            var self = this;
//            console.log("RENDER");
//            this._super();
//            this.$('.selected-mode').click(function(event){
//                self.changedMode(event,$(this));
//            });
//
//        },
    });
});
//
//var OrderlineNoteButton = screens.ActionButtonWidget.extend({
//    template: 'OrderlineNoteButton',
//    button_click: function(){
//        var line = this.pos.get_order().get_selected_orderline();
//        if (line) {
//            this.gui.show_popup('textarea',{
//                title: _t('Add Note'),
//                value:   line.get_note(),
//                confirm: function(note) {
//                    line.set_note(note);
//                },
//            });
//        }
//    },
//});