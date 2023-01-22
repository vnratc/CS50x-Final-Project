// FindPosition and GetCoordinates functions are borrowed from https://www.chestysoft.com/imagefile/javascript/get-coordinates.asp After line 33 begins my code
function FindPosition(oElement) {
    if (typeof (oElement.offsetParent) != "undefined") {
        for (var posX = 0, posY = 0; oElement; oElement = oElement.offsetParent) {
            posX += oElement.offsetLeft;
            posY += oElement.offsetTop;
        }
        return [posX, posY];
    }
    else {
        return [oElement.x, oElement.y];
    }
}

function GetCoordinates(e) {
    var PosX = 0;
    var PosY = 0;
    var ImgPos;
    ImgPos = FindPosition(myImg);
    if (!e) var e = window.event;
    if (e.pageX || e.pageY) {
        PosX = e.pageX;
        PosY = e.pageY;
    }
    else if (e.clientX || e.clientY) {
        PosX = e.clientX + document.body.scrollLeft
            + document.documentElement.scrollLeft;
        PosY = e.clientY + document.body.scrollTop
            + document.documentElement.scrollTop;
    }
    PosX = PosX - ImgPos[0];
    PosY = PosY - ImgPos[1];
    var marker = document.getElementById('marker_red')
    // Send to flask
    marker.style.visibility = "visible"
    marker.style.left = PosX + "px"
    marker.style.top = PosY + "px"
    var xy = {
        x: PosX,
        y: PosY
    }
    const request = new XMLHttpRequest()
    request.open('POST', `/processUserInfo/${JSON.stringify(xy)}`)
    request.send()
    // Clear form if clicked empty space
    document.getElementById("id").value = null
    document.getElementById("symptom").value = null
    document.getElementById("datetime").value = null
    document.getElementById("notes").value = null
    document.getElementById("marker_red").style.visibility = "visible"
    document.getElementById("button_delete").style.visibility = "hidden"
    document.getElementById("button_archive").style.visibility = "hidden"
    document.getElementById("button_activate").style.visibility = "hidden"
    document.getElementById("button-submit").disabled = false
}







