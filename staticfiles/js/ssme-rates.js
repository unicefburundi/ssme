var app = angular.module('StockApp', []);

app.controller('StockCtrl', ['$scope', '$http', function($scope, $http) {

        // province
        $http.get("/ssme/province/")
        .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
            } else {
                $("#province-group").hide();
                $http.get("/ssme/district/")
                .then(function (response) {
                    $scope.districts = response.data;
                });
            }
        });
        $scope.update_province = function () {
            var province = $scope.province;
            if (province) {
              $http.get("/ssme/district/?province__code=" + province.code)
              .then(function (response) {
                $scope.districts = response.data;
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
              });
          }
      };
        // CDS
        $scope.update_cds = function () {
            var cds = $scope.cds;
            if (cds) {
              $http.get("/ssme/cdss/" + cds.code )
              .then(function (response) {
                  $scope.etablissement = response.data.etablissements;
              });
    }
  };
}]);

