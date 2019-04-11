module.exports = {
  'env': {
    'browser': true,
    'es6': true,
  },
  'extends': [
    'eslint:recommended',
  ],
  "parserOptions": {
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  'rules': {
    'indent': [
      'error',
      2,
      {
        'SwitchCase': 1
      }
    ],
    'linebreak-style': [
      'error',
      'unix'
    ],
    'semi': [
      'error',
      'always'
    ],
    'object-curly-spacing': [
      'error',
      'always'
    ]
  }
};
