odoo.define('l10n_fr_pos_cert.pos', function (require) {
"use strict";

var models = require('point_of_sale.models');
var screens = require('point_of_sale.screens');
var core = require('web.core');
var _t = core._t;

var _super_order = models.Order.prototype;
models.Order = models.Order.extend({
	initialize: function() {
		_super_order.initialize.apply(this,arguments);
		this.send_sms = false;
	},
	export_as_JSON: function() {
		var data = _super_order.export_as_JSON.apply(this,arguments);
		data.send_sms = this.send_sms ? this.send_sms : false;
		return data
	},

	set_send_sms: function(send_sms) {
		this.send_sms = send_sms;
	},
	
	is_send_sms: function(){
		return this.send_sms;
	},
});

screens.PaymentScreenWidget.include({
	
	click_sms: function(){
		var order = this.pos.get_order();
		order.set_send_sms(!order.is_send_sms());
		this.$('.send_sms').toggleClass('highlight', order.is_send_sms());
	},

	renderElement: function() {
		var self = this;
		this._super();

		this.$('.send_sms').click(function(){
			self.click_sms();
		});
	},

	order_is_valid: function(force_validation) {
		var self = this;
		var res = this._super(force_validation);
		var order = this.pos.get_order();
		var client = order.get_client();
        if (order.is_send_sms() && (!client || client && !client.mobile)) {
            var title = !client
                ? _t('Please select the customer')
                : _t('Please provide valid Mobile No.');
            var body = !client
                ? _t('You need to select the customer before you can send the SMS.')
                : _t('This customer does not have a mobile number, define one or do not send an SMS.');
            this.gui.show_popup('confirm', {
                'title': title,
                'body': body,
                confirm: function () {
                    this.gui.show_screen('clientlist');
                },
            });
            return false;
        }
        return res
	},

});


});