const arr = [1, 2, 3, 4, 5, 6]

//MAP
function binary(x){
    return x.toString(2);
}

let output = arr.map(binary);

console.log(output);

//FILTER
function isOdd(x){
    return x % 2
}

output = arr.filter(isOdd)
console.log(output);

//REDUCE
//sum or max
output = arr.reduce(function(acc, curr){
    acc = acc + curr
    return acc;
});

console.log(output);

function findMax (arr){
    let max = 0;
    for (let i = 0; i < arr.length; i++){
        if (arr[i] > max){
            max = arr[i]
        }
    }
    return max;
}

console.log(findMax(arr));
output = arr.reduce(function(max, curr){
    if (curr > max){
        max = curr
    }
    return max
}, 0)

console.log(output);

const users = [
    {fistname: "aryan", lastname: "karki", age: 22},
    {fistname: "pratima", lastname: "shrestha", age: 24},
    {fistname: "nayra", lastname: "karki", age: 5},
    {fistname: "sharon", lastname: "karki", age: 5}
]

//list of full names
fullName = users.map((x) => x.fistname + " " + x.lastname);

console.log(fullName); 

userAge = users.reduce(function(acc, curr){
    if (acc[curr.age]){
        acc[curr.age] = ++acc[curr.age];
    }
    else{
        acc[curr.age] = 1;
    }
    return acc;
}, {});

console.log(userAge);

output = users.filter ((x) => x.age >20).map((x) => x.fistname)
console.log(output);