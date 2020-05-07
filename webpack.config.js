module.exports = {
  entry: {
    app: './static/js/src/app.js',
    'blog-feed': './static/js/src/blog-feed.js',
    'search-filters': './static/js/src/search-filters.js',
    'search-icons': './static/js/src/search-icons.js',
    'instant-page': './static/js/src/libs/instant-page/instantpage.js',
  },
  mode: process.env.ENVIRONMENT === 'devel' ? 'development' : 'production',
  output: {
    filename: '[name].min.js',
    path: __dirname + '/static/js/dist',
  },
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
    ],
  },
};
