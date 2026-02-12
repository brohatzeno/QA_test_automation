// Function Statement aka Function Decleration
function a (){
    console.log("a called ");
}
a();

// Function Expression
let b = function (){
    console.log("b called");
}
b(); //initially treated as a variable 

// Anonymous Function
function (){

}

// Named Function Expression
var c = function xyz(){
    console.log("c called");
}

// Difference between function and parameters?
function add(param1, param2){ //parameters
    console.log(param1 + param2);
}
add(4,5) //arguments
// parameters = param1, param2
// arguments = 4,5

// First class function (passing a function inside another function)
// First Class citizens
// ability of functions to be returned as values and passed as arguments
function firstClass(ano){
    console.log(ano);
}

firstClass(add());

function secondClass(){
    return function abc(){

    }
}

// Arrow function
const add = (a, b) => {
  return a + b;
};


// What is a callback function (it is called by another function)
setTimeout(function (){
    console.log("Timer");
}, 5000)

function x(y){
    console.log("x");
    y();
}
x(function y(){
    console.log("y");
})

// Javascript is a synchronous and single threaded language


// Blocking the main thread


// Power of Callbacks


// Deep about event listeners


// Closures demo with Event listeners

function attachEventListeners(){    
    let count = 0;
    document.getElementById("clickMe").addEventListener("click",function xyz(){
        console.log("ButtonClicked", ++count);
    });
}

// Scope demo with event listeners



// Garbage collection & remove Event lsteners
