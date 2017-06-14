var app = angular.module('StockApp', []);

app.controller('StockCtrl', ['$scope', '$http', function($scope, $http) {

        // province
        $http.get("/ssme/province/")
        .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
                $scope.raports = response.data;
            } else {
                $("#province-group").hide();
                $http.get("/ssme/district/")
                .then(function (response) {
                    $scope.districts = response.data;
                  $scope.raports = response.data;
                });
            }
        });
        $scope.update_province = function () {
            var province = $scope.province;
            if (province) {
              $http.get("/ssme/district/?province__code=" + province.code)
              .then(function (response) {
                $scope.districts = response.data;
                $scope.raports = response.data;
            });
          }
      };
          // district
          $scope.update_district = function () {
            var district = $scope.district;
            if (district) {
              $http.get("/ssme/cdss/?district__code=" + district.code )
              .then(function (response) {
                $scope.cdss = response.data;
                $scope.raports = response.data;
              });
          }
      };
        // CDS
        $scope.update_cds = function () {
            var cds = $scope.cds;
            if (cds) {
              $http.get("/ssme/cdss/?code=" + cds.code )
              .then(function (response) {
                $scope.raports = response.data;
              });
    }
  };
}]);

