var messageBoardApp = angular.module("messageBoardApp");  //defining a module named messageBoard
//reminder to install angular-filter via npm or bower

var api_url = "http://127.0.0.1/api/messages"

messageBoardApp.controller("ShowController", function($scope, $http){  //registering the controller with the app/module, using the controller method with the controller and a constructor method as arguements, $scope object refers to current context for the view/it is the model used by the view
  //   $scope.returnlist = function(datequery){  //returns a filtered list if an argument is passed, else shows everything
  //   	if (datequery){
  //   		datequery = "?date="+$scope.datevalue;
  //   	}
		// $http.get(api_url+datequery)
		//     .then(function(response) {
		//     	console.log("Searched data successfully")
		//         $scope.items = response.data;
		//     },
		//     function(error) {
		//     	console.log(error)
		//     });
  //   }

    $scope.searchdata = function() {
		$http.get(api_url+"?date="+$scope.datevalue)
		    .then(function(response) {
		    	console.log("Searched data successfully")
		        $scope.items = response.data;
		    },
		    function(error) {
		    	console.log(error)
		    });
	}

	$http.get(api_url)
		.then(function(response) {
			console.log("Received data successfully")  //debugging code
			$scope.items = response.data;
		},
		function(error) {
			console.log(error)
		});
});

messageBoardApp.controller("PostController", function($scope, $http){
	$scope.postdata = function() {
        var data = {
        	"message": $scope.message
        } //for the key to post inthe http method
		$http.post(api_url, JSON.stringify(data))
			.then(function(response) {
				$scope.items.push(response.data);
				console.log("Posted data successfully")  //this message is not showing

			},
			function(error) {
				console.log(error)
			});
	}
})

// messageBoardApp.controller("SearchController", function($scope, $http){
// 	$scope.searchdata = function() {
// 		$http.get("http://127.0.0.1/api/messages?date="+$scope.datevalue)
// 		    .then(function(response) {
// 		    	console.log("Searched data successfully")
// 		        $scope.items = response.data;
// 		    },
// 		    function(error) {
// 		    	console.log(error)
// 		    });
// 	}
// })
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