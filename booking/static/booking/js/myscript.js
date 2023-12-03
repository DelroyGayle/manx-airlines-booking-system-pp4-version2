/*jshint esversion: 11 */

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

// This function is used by the <script></script> block below
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
            idElement = $( `#id_child-${paxno}-title` );
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
    // Then add a Heading to each set of Adults, Children and Infants
    const titlePresent = $( "#id_adult-0-title" );
    if (titlePresent.length) {
        add_headings_to_pax(titlePresent);
    }

    /* Adult 1 Passenger is a Mandatory part of the Booking
       Adult 1 cannot be removed - therefore disable and hide the option
    */
    
    const adult0 = document.getElementById("id_adult-0-remove_pax");
    if (adult0) {
        adult0.disabled = true;
        adult0.hidden=true;
        $('label[for="id_adult-0-remove_pax"]').hide();
    }    
}

/*
If checked, strike-thru
Id not checked, remove strike-thru
*/
function toggleStrikeThru(theActualElement, elementStringId) {
       // Construct element's First Name ID
       let elementFirstName = `${elementStringId}first_name`;
       elementFirstName = document.getElementById(elementFirstName);
       // Construct element's Last Name ID
       let elementLastName = `${elementStringId}last_name`;
       elementLastName = document.getElementById(elementLastName);

       if (theActualElement.checked) {
            // Cross Out The Names
            elementFirstName.classList.add("strike-thru");
            elementLastName.classList.add("strike-thru");
        } else {
            // Restore The Names
            elementFirstName.classList.remove("strike-thru");
            elementLastName.classList.remove("strike-thru");
        }      
}

function setTheInfant(infantElement, adultElement, elementStringId, thenumber) {
    
       if (!infantElement) {
            // There is no corresponding Infant Element
            // Therefore, update the Adult Element Only
            toggleStrikeThru(adultElement, elementStringId);
            return;
       }
    
       if  ((adultElement.checked && infantElement.checked) ||
            (!adultElement.checked && !infantElement.checked)) {
                // do nothing
            } else {
                // Ensure that both elements are in sync
                infantElement.click();
            }

       // Construct Adult's First Name ID
       let adultFirstName = `id_adult-${thenumber}-first_name`;
       adultFirstName = document.getElementById(adultFirstName);
       // Construct Adult's Last Name ID
       let adultLastName = `id_adult-${thenumber}-last_name`;
       adultLastName = document.getElementById(adultLastName);
       // Construct infant's First Name ID
       let infantFirstName = `id_infant-${thenumber}-first_name`;
       infantFirstName = document.getElementById(infantFirstName);
       // Construct infant's Last Name ID
       let infantLastName = `id_infant-${thenumber}-last_name`;
       infantLastName = document.getElementById(infantLastName);

       if (adultElement.checked) {
            // Cross Out The Names
            adultFirstName.classList.add("strike-thru");
            adultLastName.classList.add("strike-thru");
            infantFirstName.classList.add("strike-thru");
            infantLastName.classList.add("strike-thru");
        } else {
            // Restore The Names
            adultFirstName.classList.remove("strike-thru");
            adultLastName.classList.remove("strike-thru");
            infantFirstName.classList.remove("strike-thru");
            infantLastName.classList.remove("strike-thru");
        }      
}

const openTooManyInfantsModal = () => {
    $(".ui.modal.toomanyinfants").modal("show");
};

$(document).ready( function() {
    checkReturnFlightOption();
});

document.addEventListener('click',function(e) {
    /* Check for id_adult-N-remove_pax
       where N is >=1
       
       FOR ZERO:
       id_adult-0-remove_pax is both disabled and hidden
    */

       let pattern = /^id_adult-([0-9]+)-remove_pax$/;
    
        if (e.target && pattern.test(e.target.id)) {
            // A matching Adult element's checkbox was clicked
            const adultId = e.target.id;
            const adultElement = e.target;
            const thenumber = pattern.exec(adultId);
            const elementStringId = `id_adult-${thenumber[1]}-`; // e.g. "id_adult-1-"
            const infantId = `id_infant-${thenumber[1]}-remove_pax`;
            const infantElement = document.getElementById(infantId);
            // Ensure the corresponding Infant element corresponds with the Adult
            setTheInfant(infantElement, adultElement, elementStringId, thenumber[1]);
            return;
        }

    /* Check for 'id_child-N-remove_pax' OR for 'id_infant-N-remove_pax'
       where N is >=0       
    */

        pattern = /^(id_(child|infant)-([0-9]+)-)remove_pax$/;
    
        if (e.target && pattern.test(e.target.id)) {
            // A matching element's checkbox was clicked
            const theId = e.target.id;
            const theElement = e.target;
            const theMatched = pattern.exec(theId);
            const theStringId = theMatched[1]; // e.g. "id_child-0-"
            toggleStrikeThru(theElement, theStringId);
            return;
        }
    }
 );

// This solution regarding .ready() not triggering when Back Button pressed was found at
// https://stackoverflow.com/questions/11871253/execute-document-ready-even-if-user-came-to-the-page-by-hitting-the-back-button

$(window).on("pageshow", function() {
    checkReturnFlightOption();
    setup_page();
});