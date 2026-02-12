// let myName = "aryan";

// let yourName = prompt("What is your name?");
// alert("Hii, my name is " + myName + "!" + " Welcome to our website " + yourName );

// let message = "Hello"
// let Fname = "Aryan"

// alert(message + " " + Fname)




// SLICING
// let Fname = "Aryan"
// console.log(Fname.slice(4,5));

// let tweet = prompt("Compose your tweet: ");
// let tweetCount = tweet.length;
// let tweetLim = tweet.slice(0,140)

// if (tweetCount <= 140){
//     alert("You have written " + tweetCount + " chatacters, you have " + (140 - tweetCount) + " characters remaining.")
// }
// else if (tweetCount > 140){
//     alert("You exceeded the character count! \n \n \n" + tweetLim)

// }


// UPPER CASE
// let namme = "Aryan"
// console.log(namme.toUpperCase());
// console.log(namme.toLowerCase());

// let fname = prompt("What is your name: ")
// console.log("Hello " + (fname.slice(0,1)).toUpperCase() + (fname.slice(1,)).toLowerCase()+ " Welcome to the website");




// DOG AGE INTO HUMAN AGE
// let dogAge = prompt("How old is your dog: ")
// let humanAge = (dogAge - 2) * 4 + 21

// console.log("Your dog's age in Human years is " + humanAge);


// CALL STACK
// let x = 1;
// a();
// b();
// console.log(x);

// function a (){
//     let x = 10;
//     console.log(x);
// }

// function b (){
//     let x = 100;
//     console.log(x);
// }



// LEXICAL ENVIRONMENT // SCOPE CHAIN
function a(){
    let b = 10;
    function c(){
        console.log(b);
    }
}
a();
console.log(b);