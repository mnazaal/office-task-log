var messageBoardApp = angular.module("messageBoardApp", []);  //defining a module named messageBoard

messageBoardApp.controller("MessageController", ['$scope', function($scope, $http){  //registering the controller with the app/module, using the controller method with the controller and a constructor method as arguements, $scope object refers to current context for the view/it is the model used by the view
	$scope.items = [];

	console.log($scope.items)
	
	$scope.getMessages = function() {
		$http.get("127.0.0.2:8080/messages")
		.then(function(response) {
			$scope.items = response.data;
			console.log("success")
		});
	};
}]);

// 	var webapp = this;
// 	webapp.title = "Event log";
// 	webapp.posts = {};
// 	$scope.message = "The variable is showing"; //declaring variable message which can be used in the view now
// 	$scope.testmethod1 = function(){
// 		console.log("This button1 works");
// 	}
// 	$scope.testmethod2 = function(){
// 		console.log("This button2 works");
// 	}		
// });

// try {
//     // Opera 8.0+, Firefox, Safari 
//     ajaxRequest = new XMLHttpRequest();
// } catch (e)