// FindPosition and GetCoordinates functions are borrowed from https://www.chestysoft.com/imagefile/javascript/get-coordinates.asp



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

var x_db = 0
var y_db = 0
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
    x_db = PosX,
    y_db = PosY

    let xy = {
        x : x_db,
        y : y_db
    }
    
    let marker = document.getElementById('marker')
    let o = 0 // Offset to center the marker where the click is.
    
    myImg.addEventListener('click', function () {
        marker.style.visibility = "visible"
        marker.style.left = PosX - o + "px"
        marker.style.top = PosY - o + "px"
    });
    
    console.log(xy)
    const request = new XMLHttpRequest()
    request.open('POST', `/processUserInfo/${JSON.stringify(xy)}`)
    request.send()
    
    document.getElementById("x").innerHTML = PosX - o;
    document.getElementById("y").innerHTML = PosY - o;
    // console.log(x_db)
    // console.log(y_db)
}


