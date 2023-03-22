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
    ImgPos = FindPosition(myImg[0]);
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
    marker.style.left = PosX - 10 + "px"    // 10 is the offset to position marker exactly where the click is, because marker is 20x20px
    marker.style.top = PosY - 10 + "px"
    var xy = {
        x: PosX,
        y: PosY
    }
    const request = new XMLHttpRequest()
    request.open('POST', `/processUserInfo/${JSON.stringify(xy)}`)
    request.send()
    // Clear form if clicked empty space
    let fields = document.querySelectorAll('#id, #symptom, #datetime, #notes')
    for (f of fields) {f.value = null}
    document.getElementById("marker_red").style.visibility = "visible"
    let elHide = document.querySelectorAll('#button_delete, #button_archive, #button_activate')
    for (el of elHide) {el.style.visibility = 'hidden'}
    document.getElementById("button-submit").disabled = false
    // Remove highlight from other markers
    let markers_visible = document.querySelectorAll('.markers_visible, .markers_hidden')
    for (m of markers_visible) (m.style.border = '0px')
}







