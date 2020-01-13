module.exports = {
  entry: {
    app: './assets/js/src/app.js',
    'blog-feed': './assets/js/src/blog-feed.js',
    'search-filters': './assets/js/src/search-filters.js',
    'search-icons': './assets/js/src/search-icons.js'
  },
  mode: process.env.ENVIRONMENT === 'devel' ? 'development' : 'production',
  output: {
    filename: '[name].min.js',
    path: __dirname + '/assets/js/dist'
  },
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      }
    ]
  }
};
