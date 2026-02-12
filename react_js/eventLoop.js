// console.log("Start");
// setTimeout(function cbT(){
//     console.log("CB Timeout");
// }, 5000);

// fetch("http://api.netflix.com")
// .then(function cbF(){
//     console.log("CB Netflix");
// });

// console.log("End");


console.log("Start");

setTimeout(function cb(){
    console.log("Callback");
}, 5000);

console.log("End");

//million
let startDate = new Date().getTime();
let endDate = startDate;

while(endDate <startDate + 10000) {
    endDate = new Date().getTime();
}

console.log("While expires");
