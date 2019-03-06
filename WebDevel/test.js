"use strict";

let seats = document.createElement("p");
document.body.appendChild(seats);
seats.innerHTML = "Namn att leta efter";

let seatsInput= document.createElement("input");
document.body.appendChild(seatsInput);
seatsInput.focus();

let limit = document.createElement("p");
document.body.appendChild(limit);
limit.innerHTML = "Plats att leta på";

let limitInput= document.createElement("input");
document.body.appendChild(limitInput);
 
let button = document.createElement("button");
document.body.appendChild(button);
button.style.marginLeft = "10px";
button.innerHTML="Hitta!";
button.onclick = click;

let res= document.createElement("p");
document.body.appendChild(res);

let CallerId = "Lag1";

function click() {
    let Random = (Math.random().toString(36).substr(2, 9) + Math.random().toString(36).substr(2, 9)).substr(0, 16);
    let Time = Date.now();
    let lenght = Random.length;

    res.innerHTML = "Personen har nummer: " + Random + " Antal tecken = " + lenght + " timestamp = " + Time;
}

