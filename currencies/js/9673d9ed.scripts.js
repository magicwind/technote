'use strict';
// Declare app level module which depends on filters, and services
angular.module('myApp', [
  'myApp.filters',
  'myApp.services',
  'myApp.directives'
]);
'use strict';
/* Services */
//This Service provides game objects
var servicesModule = angular.module('myApp.services', ['ngResource']);
servicesModule.factory('openExchangeRates', [
  '$resource',
  function ($resource) {
    return $resource('https://openexchangerates.org/api/:path', {
      callback: 'JSON_CALLBACK',
      app_id: '5c2dba0f887544a4b196eeaa8a3052f4'
    }, {
      getRates: {
        method: 'JSONP',
        params: { path: 'latest.json' }
      },
      getLegend: {
        method: 'JSONP',
        params: { path: 'currencies.json' }
      }
    });
  }
]);
servicesModule.factory('localService', [
  '$resource',
  function ($resource) {
    return $resource('localService/:path', {}, {
      getCurrencies: {
        method: 'GET',
        params: { path: 'currencies.json' }
      }
    });
  }
]);
'use strict';
/* Controllers */
function currencyCrtl($scope, openExchangeRates, localService) {
  $scope.balances = new Array();
  $scope.exchangeRates = openExchangeRates.getRates();
  $scope.currencyLegend = localService.getCurrencies();
  $scope.amountChanged = function (changedBalance) {
    //console.log(changedBalance);
    if (Number(changedBalance.amount) === 0) {
      return;
    }
    var baseValue = $scope.convertCurrencyValueToBaseValue(changedBalance.amount, changedBalance.exchangeRate);
    _.each($scope.balances, function (balance, index) {
      if (changedBalance.$$hashKey !== balance.$$hashKey && typeof balance.exchangeRate === 'number') {
        balance.amount = $scope.roundDown($scope.convertBaseValueToCurrencyValue(baseValue, balance.exchangeRate));
      }
    });
  };
  $scope.currencyChanged = function (changedBalance) {
    //console.log(changedBalance);
    _.each($scope.balances, function (balance, index) {
      if (changedBalance.$$hashKey !== balance.$$hashKey && Number(balance.amount) > 0) {
        // update this currency's amount according to the base value
        var baseValue = $scope.convertCurrencyValueToBaseValue(balance.amount, balance.exchangeRate);
        changedBalance.amount = $scope.roundDown($scope.convertBaseValueToCurrencyValue(baseValue, changedBalance.exchangeRate));
        // end loop
        return false;
      }
    });
  };
  $scope.addBalance = function () {
    var newEmptyBalance = {
        exchangeRate: '',
        amount: ''
      };
    $scope.balances.push(newEmptyBalance);
  };
  $scope.removeBalance = function (index) {
    $scope.balances.splice(index, 1);
  };
  $scope.getCurrencyName = function (symbol) {
    if ($scope.currencyLegend) {
      return $scope.currencyLegend[symbol];
    } else {
      return false;
    }
  };
  $scope.getCurrencyNameFull = function (symbol) {
    if ($scope.currencyLegend) {
      return $scope.currencyLegend[symbol] + ' (' + symbol + ')';
    } else {
      return false;
    }
  };
  $scope.totalBalance = function () {
    var total = 0;
    for (var m = 0; m < $scope.balances.length; m++) {
      var value = $scope.convertToNumber($scope.balances[m].amount);
      var exchangeRate = $scope.balances[m].exchangeRate;
      if (value != 0 && exchangeRate != '') {
        //total = total + value;
        total = total + $scope.convertCurrencyValueToBaseValue(value, exchangeRate);
      }
    }
    return total;
  };
  $scope.convertToNumber = function (value) {
    var floatNumber = parseFloat(value);
    if (floatNumber) {
      return floatNumber;
    } else {
      return 0;
    }
  };
  $scope.roundDown = function (number) {
    return Math.round(number * 100) / 100;
  };
  $scope.convertCurrencyValueToBaseValue = function (currencyValue, exchangeRate) {
    var baseValue = currencyValue / exchangeRate;
    return baseValue;
  };
  $scope.convertBaseValueToCurrencyValue = function (baseValue, exchangeRate) {
    var currencyValue = baseValue * exchangeRate;
    return currencyValue;
  };
  $scope.ageOfExchangeRate = function () {
    if ($scope.exchangeRates) {
      var currentTimeStamp = new Date().getTime();
      // multiplied by 1000 so that the argument is in milliseconds, not seconds
      var ageOfExchangeRate = currentTimeStamp - $scope.exchangeRates.timestamp * 1000;
      var minutes = Math.round(ageOfExchangeRate / 1000 / 60);
      var formattedTime = minutes + ' minutes';
      return formattedTime;
    } else {
      return false;
    }
  };
  // populate form on load with two empty fields
  $scope.addBalance();
  $scope.addBalance();  //Socialite.load('social-buttons');
}
'use strict';
/* Filters */
angular.module('myApp.filters', []).filter('interpolate', [
  'version',
  function (version) {
    return function (text) {
      return String(text).replace(/\%VERSION\%/gm, version);
    };
  }
]);
angular.module('myApp.filters', []).filter('usedCurrencies', function () {
  return function (currencies) {
    var newRates = {};
    var usedCurrencies = [
        'CNY',
        'HKD',
        'USD',
        'JPY',
        'KRW',
        'TWD',
        'MOP',
        'AUD',
        'EUR'
      ];
    angular.forEach(currencies, function (value, key) {
      if (_.indexOf(usedCurrencies, key) >= 0) {
        newRates[key] = value;
      }
    });
    return newRates;
  };
});
'use strict';
/* Directives */
angular.module('myApp.directives', []).directive('appVersion', [
  'version',
  function (version) {
    return function (scope, elm, attrs) {
      elm.text(version);
    };
  }
]);
