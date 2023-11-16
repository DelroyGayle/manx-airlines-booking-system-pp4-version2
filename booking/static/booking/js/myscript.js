
function returnCheck() {
    let theReturn = document.getElementById("id_return_option").value;
    setValue = (theReturn === "N") ? true : false;
    // Hide/Show elements depending on 'theReturn'
    document.getElementById("id_returning_date").hidden = setValue;
    document.getElementById("id_returning_time").hidden = setValue;
}

function adultsCheck() {
/* TODO */
}

function childrenCheck() {
    /* TODO */
}
    
function infantsCheck() {
    
    let infantsValue = Number(document.getElementById("id_infants").value);
    let adultsValue = Number(document.getElementById("id_adults").value);
    // Defensive Code
    if (!Number.isInteger(infantsValue)) {
        infantsValue = 0
        document.getElementById("id_infants").value="0"
    }
    if (!Number.isInteger(adultsValue)) {
        adultsValue = 1
        document.getElementById("id_adults").value="1";
    }

    // Check that number of infants does NOT exceed the number of infants
    if (infantsValue > adultsValue)
    {
        openTooManyInfantsModal();
        document.getElementById("id_infants").focus();
        return false // Indicate Test Failure
    }

    return true  // Indicate Test Success
}

function leavePageValidation() {
    // Check that there is at least one adult
    // (However the 'minimum value' of #id_adults is set to 1)
    let adultsValue = Number(document.getElementById("id_adults").value);
    alert((adultsValue === 0 || true))
    if (adultsValue === 0 || true)
    {
        openNoAdultsModal();
        document.getElementById("id_adults").focus();
        event.preventDefault();
        return false // Indicate Test Failure
    }
}

const openTooManyInfantsModal = () => {
    $('.ui.modal.toomanyinfants').modal('show');
}

const openNoAdultsModal = () => {
    $('.ui.modal.no_adults').modal('show');
}