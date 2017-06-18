var app = angular.module('StockApp', []);

app.controller('StockCtrl', ['$scope', '$http', function($scope, $http) {

        // campaign
        $http.get("/ssme/campaign/")
        .then(function (response) {
            if (response.data.length > 0) {
                $scope.campaigns = response.data;
            }
        });

        $scope.update_campaign = function () {
            $scope.days = null;
            var campaign = $scope.campaign;
            if (campaign) {
                $scope.days = campaign.days;
        }
      };

      $scope.update_day = function () {
            var day = $scope.day;
            if (day) {
                $http.get("/ssme/province/?dates=" + day )
                  .then(function (response) {
                      if (response.data.length > 0) {
                          $scope.provinces = response.data;
                          $scope.raports = response.data;
                          $scope.districts = null;
                          $scope.cdss = null;
                      }
                       
                  });
        }
      };

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
            if (province && $scope.day != null) {
              $http.get("/ssme/district/?province__code=" + province.code + "&dates=" +  $scope.day)
              .then(function (response) {
                $scope.districts = response.data;
                $scope.raports = response.data;
                $scope.cdss = null;

          });
        } else {
          $http.get("/ssme/district/?province__code=" + province.code)
              .then(function (response) {
                $scope.districts = response.data;
                $scope.raports = response.data;
                $scope.cdss = null;

          });
        }
      };
          // district
          $scope.update_district = function () {
            var district = $scope.district;
            if (district && $scope.day != null) {
              $http.get("/ssme/cdss/?district__code=" + district.code + "&dates=" +  $scope.day)
              .then(function (response) {
                $scope.cdss = response.data;
                $scope.raports = response.data;
          });
        } else {
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
            if (cds && $scope.day != null) {
              $http.get("/ssme/cdss/?code=" + cds.code + "&dates=" +  $scope.day)
              .then(function (response) {
                $scope.raports = response.data;
              });
            } else {
              $http.get("/ssme/cdss/?code=" + cds.code + "&dates=" )
              .then(function (response) {
                $scope.raports = response.data;
              });
            }
          };
}]);

