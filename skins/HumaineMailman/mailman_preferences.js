/*
Project: HumaineMailman
 Author: Christian Federmann <cfedermann@gmail.com>

This work has been supported by the EC Project HUMAINE (IST-507422);
See http://emotion-research.net/ for more information.
*/

function check_all() {
    checkboxes = document.mailman_member_preferences_form.checkboxes.value;
    for(i=0;i<checkboxes;i++) {
        eval('document.mailman_member_preferences_form.checkbox_' + i + '.checked=true;');
    }
}

function uncheck_all() {
    checkboxes = document.mailman_member_preferences_form.checkboxes.value;
    for(i=0;i<checkboxes;i++) {
        eval('document.mailman_member_preferences_form.checkbox_' + i + '.checked=false;');
    }
}

function invert_all() {
    checkboxes = document.mailman_member_preferences_form.checkboxes.value;
    for(i=0;i<checkboxes;i++) {
        code = 'document.mailman_member_preferences_form.checkbox_' + i + '.checked=';
        code += '!(document.mailman_member_preferences_form.checkbox_' + i + '.checked);';
        eval(code);
    }
}