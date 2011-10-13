// Methods to make the timepicking concise (cant select start time > end time and vice-versa)

// They were modified from the plugin example to make them reusable - the callbacks receives the name of the related
// timepicker.

function tpStartOnHourShowCallback(hour, tpEndName) {
    var tpEndHour = $('#' + tpEndName).timepicker('getHour');
    // Check if there is any hour selected on the other picker
    if (tpEndHour == -1) { return true; }
    // Check if proposed hour is prior or equal to selected end time hour
    if (hour <= tpEndHour) { return true; }
    // if hour did not match, it can not be selected
    return false;
};
function tpStartOnMinuteShowCallback(hour, minute, tpEndName) {
    var tpEndHour = $('#' + tpEndName).timepicker('getHour');
    var tpEndMinute = $('#' + tpEndName).timepicker('getMinute');
    // Check if there is any hour/minute selected on the other picker
    if (tpEndHour == -1 && tpEndMinute == -1) { return true; }
    // Check if proposed hour is prior to selected end time hour
    if (hour < tpEndHour) { return true; }
    // Check if proposed hour is equal to selected end time hour and minutes is prior
    if ( (hour == tpEndHour) && (minute < tpEndMinute) ) { return true; }
    // if minute did not match, it can not be selected
    return false;
};
function tpEndOnHourShowCallback(hour, tpStartName) {
    var tpStartHour = $('#' + tpStartName).timepicker('getHour');
    // Check if there is any hour selected on the other picker
    if (tpStartHour == -1) { return true; }
    // Check if proposed hour is after or equal to selected start time hour
    if (hour >= tpStartHour) { return true; }
    // if hour did not match, it can not be selected
    return false;
};
function tpEndOnMinuteShowCallback(hour, minute, tpStartName) {
    var tpStartHour = $('#' + tpStartName).timepicker('getHour');
    var tpStartMinute = $('#' + tpStartName).timepicker('getMinute');
    // Check if there is any hour/minute selected on the other picker
    if (tpStartHour == -1 && tpStartMinute == -1) { return true; }
    // Check if proposed hour is after selected start time hour
    if (hour > tpStartHour) { return true; }
    // Check if proposed hour is equal to selected start time hour and minutes is after
    if ( (hour == tpStartHour) && (minute > tpStartMinute) ) { return true; }
    // if minute did not match, it can not be selected
    return false;
};

        // Proxies to make callbacks reusable :)
        function tpStartOnHourShowCallbackProxy(hour){
            tpStartOnHourShowCallback(hour, 'id_time_end');
        };
        function tpStartOnMinuteShowCallbackProxy(hour, minute){
            tpStartOnMinuteShowCallback(hour, minute, 'id_time_end');
        };
        function tpEndOnHourShowCallbackProxy(hour){
            tpEndOnHourShowCallback(hour, 'id_time_start');
        };
        function tpEndOnMinuteShowCallbackProxy(hour, minute){
            tpEndOnMinuteShowCallback(hour, minute, 'id_time_start');
        }