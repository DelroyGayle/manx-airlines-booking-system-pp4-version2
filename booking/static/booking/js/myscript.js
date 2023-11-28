// Hide/Show elements depending on '#theReturn'

function hide_returning_option() {
    $("span:contains('DD/'):nth-of-type(2)").hide();
    $("label:contains('Returning'):nth-of-type(2)").hide();
    $('label[for="id_returning_date"]').hide();
    $("#id_returning_date").hide();
    $('label[for="id_returning_time_0"]').hide();
    $("#id_returning_time").hide();
}

function show_returning_option() {
    $("span:contains('DD/'):nth-of-type(2)").show();
    $("label:contains('Returning'):nth-of-type(2)").show();
    $('label[for="id_returning_date"]').show();
    $("#id_returning_date").show();
    $('label[for="id_returning_time_0"]').show();
    $("#id_returning_time").show();
}

function returnCheck() {
    let theReturn = document.getElementById("id_return_option").value;
    if (theReturn === "N") {
        hide_returning_option();
    } else {
        show_returning_option();
    }
}

function infantsCheck() {
    let infantsValue = Number(document.getElementById("id_infants").value);
    let adultsValue = Number(document.getElementById("id_adults").value);
    // Defensive Code
    if (!Number.isInteger(infantsValue)) {
        infantsValue = 0;
        document.getElementById("id_infants").value = "0";
    }
    if (!Number.isInteger(adultsValue)) {
        adultsValue = 1;
        document.getElementById("id_adults").value = "1";
    }

    // Check that number of infants does NOT exceed the number of infants
    if (infantsValue > adultsValue) {
        openTooManyInfantsModal();
        document.getElementById("id_infants").focus();
        return false; // Indicate Test Failure
    }

    return true; // Indicate Test Success
}

function checkReturnFlightOption() {
    if ($("#id_returning_date").length) {
        returnCheck();
    }
}

function add_heading(idElement, number, heading) {
        adultNumber = `${heading} $(number)`;
        idElement.parent().before( `<h3 class=\"ui centered header\"><em>${heading} ${number}</em></h3>` );
}

// Add headings to each set of Adults, Children and Infants
function add_headings_to_pax(idElement) {
    // Already pointing to the first passenger type
    let paxno = 0;
    do {
        add_heading(idElement, paxno + 1, "Adult");
        paxno++;
        idElement = $( `#id_adult-${paxno}-title` );
    } while (idElement.length);

    // Any children?
    idElement = $( "#id_child-0-title" );
    if (idElement.length) {
        paxno = 0;
        do {
            add_heading(idElement, paxno + 1, "Child");
            paxno++;
            idElement = $( `#id_child-${paxno}-title` )
        } while (idElement.length);
    }

    // Any infants?
    idElement = $( "#id_infant-0-title" );
    if (idElement.length) {
        paxno = 0;
        do {
            add_heading(idElement, paxno + 1, "Infant");
            paxno++;
            idElement = $( `#id_infant-${paxno}-title` );
        } while (idElement.length);
    }
}

function setup_page() {
    // If it is a page showing the Passenger Types
    // Then Add a heading to each set of Adults, Children and Infants
    console.log("TEST")
    let p = $( "#id_adult-0-title" )
    if (p.length) {
        add_headings_to_pax(p)
    }
    console.log("OK2")

    // labelText = $('label[for="id_adult_0_remove_pax"]').css("color", "red")
    console.log("OK")
    $( "id_adult-0-remove_pax" ).prop("disabled", true)

    document.getElementById("id_adult-0-remove_pax").disabled = true;
    document.getElementById("id_adult-0-remove_pax").hidden=true;
}

const openTooManyInfantsModal = () => {
    $(".ui.modal.toomanyinfants").modal("show");
}

const openNoAdultsModal = () => {
    $(".ui.modal.no_adults").modal("show");
}


$(document).ready( function() {
    checkReturnFlightOption();
});

// This solution regarding .ready() not triggering when Back Button pressed was found at
// https://stackoverflow.com/questions/11871253/execute-document-ready-even-if-user-came-to-the-page-by-hitting-the-back-button

$(window).on("pageshow", function() {
    checkReturnFlightOption();
    setup_page();
    // document.getElementById("id_adult-0-pax-remove_pax").disabled = true;
});

// <input type="checkbox" name="adult-0-remove_pax" id="id_adult-0-remove_pax"></input>