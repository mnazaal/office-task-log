console.log("/var/www/logapp/static/app.js");

var messageBoardApp = angular.module("messageBoardApp", ['angular.filter']);  //defining a module named messageBoard
//reminder to install angular-filter via npm or bower

messageBoardApp.controller("ShowController", function($scope, $http){  //registering the controller with the app/module, using the controller method with the controller and a constructor method as arguements, $scope object refers to current context for the view/it is the model used by the view
	var searchbutton = document.getElementById("date");
	console.log(searchbutton)

	$http.get("http://127.0.0.1/api/messages")
		.then(function(response) {
			$scope.items = response.data;
			console.log("Received data successfully")  //debugging code
		},
		function(error) {
			console.log(error)
		});
});

messageBoardApp.controller("PostController", function($scope, $http){
	$scope.postdata = function(message){
		var date = new Date();  //getting current date
		$scope.datestring = date.getFullYear() + '-' + ('0' + (date.getMonth() + 1)).slice(-2) + '-' + ('0' + date.getDate()).slice(-2);
		var data = {
			date: $scope.datestring,
			username: "nazaal", //also gonna fix soon
			message: message,
			time: "right now"  //gonna fix soon
		}
		$http.post('api/messages', JSON.stringify(data))
			.then(function(response) {
				if (response.data)
				console.log("Post data send successfully");
			},
			function(error) {
				console.log(error)
			});
	}
})
//routeparams

// messageBoardApp.controller("SearchController", function($scope, $http){
// 	$scope.search = [];
// 	var searchbutton = document.getElementById("date");
// 	console.log(searchbutton)

// 	$http.get("http://127.0.0.2:8080/messages")
// 		.then(function(response) {
// 			$scope.search = response.data
// 			console.log("success searched list")  //debugging code
// 		},
// 		function(error) {
// 			console.log(error)
// 		});
// });

// messageBoardApp.controller("SearchController", function($http, $scope, $filter) {
// 	var jsonlist = $http.get("http://127.0.0.2:8080/messages")
// 	$scope.searched = $filter('filter')(jsonlist, function (i) {return i.date === $scope.datevalue;})[0];
// })