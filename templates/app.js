angular.module("messageBoardApp", []);  //defining a module named messageBoard

messageBoardApp.controller("MessageBoardController", function($scope){  //registering the controller with the app/module, using the controller method with the controller and a constructor method as arguements, $scope object refers to current context for the view/it is the model used by the view
	$scope.message = "The variable is showing", //declaring variable message which can be used in the view now
	$scope.testmethod1 = function() {
		console.log("This button1 works");
	}
	$scope.testmethod2 = function() {
		console.log("This button2 works");
	}
		
});

// try {
//     // Opera 8.0+, Firefox, Safari 
//     ajaxRequest = new XMLHttpRequest();