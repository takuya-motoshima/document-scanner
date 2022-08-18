const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const path = require('path');
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

module.exports = {
  watchOptions: {
    aggregateTimeout: 300,
    poll: 1500,
    ignored: [
      path.resolve(__dirname, 'src/theme'),
      path.resolve(__dirname, 'src/media'),
      path.resolve(__dirname, 'node_modules')
    ]
  },

  // Main JavaScript file (entry point).
  entry: {
    docs: './src/pages/docs.js',
    ocr: './src/pages/ocr.js',
    minorCheck: './src/pages/minorCheck.js'
  },

  // File output settings.
  output: {
    // Output file directory name.
    path: path.resolve(__dirname, '../public/build'),
    // Output file name.
    filename: '[name].js'
  },
  plugins: [
    // new webpack.ProvidePlugin({moment: 'moment'}),
    new MiniCssExtractPlugin(),
    new CopyPlugin({
      patterns: [
        {from: 'src/media', to: 'media'},
        {from: 'src/theme', to: 'theme'}
      ]
    })
  ],
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {url: false}
          }
        ]
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {url: false}
          },
          {
            loader: 'sass-loader'
          }
        ]
      }
    ]
  },
  optimization: {
    minimizer: [
      new CssMinimizerPlugin()
    ]
  },

  // Do not include React itself in the bundle file.
  externals: {
    jquery: 'jQuery'
  },
  resolve: {
    extensions: ['.js'],
    alias: {
      '~': path.resolve(__dirname, 'src')
    }
  },
  performance: {
    maxEntrypointSize: 512000,
    maxAssetSize: 5242880
  }
};