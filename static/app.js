var messageBoardApp = angular.module("messageBoardApp", ['angular.filter']);  //defining a module named messageBoard
//reminder to install angular-filter via npm or bower

messageBoardApp.controller("MessageController", function($scope, $http){  //registering the controller with the app/module, using the controller method with the controller and a constructor method as arguements, $scope object refers to current context for the view/it is the model used by the view

	$http.get("http://127.0.0.2:8080/messages")
		.then(function(response) {
			$scope.items = response.data;
			console.log("success whole list")  //debugging code
		},
		function(error) {
			console.log(error)
		});
});

//routeparams
