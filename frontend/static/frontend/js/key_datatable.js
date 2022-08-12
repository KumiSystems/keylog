function editkey(element) {
    var keyid = $(element).parent().parent().parent().children()[1].innerText;
    document.location.href = keyid + "/edit/";
};

function usekey(element) {
    var keyid = $(element).parent().parent().parent().children()[1].innerText;
    document.location.href = keyid + "/use/";
};