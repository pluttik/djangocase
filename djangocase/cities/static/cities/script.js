$(document).ready(
//this function couples the select#cities menu to the select#hotel menu
function() {
    $("select#cities").change(function() {
    if ($(this).val() == 'Z') {
        $("select#hotel").html("<option>Select a hotel:</option>");
        $("select#hotel").attr('disabled', true);
    }
    else {
        var url = "/cities/" + $(this).val() + "/all_json_hotels";
        var city_name = $(this).val();
        $.getJSON(url, function(hotels) {
            var options = '<option value="Z">Select a hotel:</option>';
            for (var i = 0; i < hotels.length; i++) {
                options += '<option value="' + hotels[i].pk + '">' + hotels[i].fields['hotel_name'] + '</option>';
            }
            $("select#hotel").html(options);
            $("select#hotel option:first").attr('selected', 'selected');
            $("select#hotel").attr('disabled', false);
        });
    }
    });
    
    $("select#model").change(function(vent) {
        if ($(this).val() == -1) {
            return;
}
});
});
