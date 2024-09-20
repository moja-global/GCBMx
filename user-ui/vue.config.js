const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack')

module.exports = defineConfig({
  devServer: {
    port: 8000
  },
  runtimeCompiler: true,
  transpileDependencies: true,
  configureWebpack: {
    plugins: [
      // fix "process is not defined" error:
      new webpack.ProvidePlugin({
        process: 'process/browser',
      }),
    ],
    resolve: {
      fallback: {
        path: require.resolve('path-browserify'),
        crypto: require.resolve('crypto-browserify'),
        stream: require.resolve('stream-browserify'),
        process: require.resolve('process/browser'),
        vm: require.resolve("vm-browserify"),
        // Add other fallbacks if needed
        // e.g., fs: false, os: false, stream: require.resolve('stream-browserify')
      }
    }
  }
});
