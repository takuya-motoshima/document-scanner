const PORT = 3004;

module.exports = {
  apps : [
    {
      name: 'document-scanner',
      script: 'bin/www',
      exec_mode: 'cluster_mode',
      watch: '.',
      watch_delay: 3000,
      ignore_watch : [
        'node_modules',
        'public',
        'views',
        'client',
        'logs'
      ],
      watch_options: {
        followSymlinks: false,
        usePolling: true
      },
      env: {
        NODE_ENV: 'development',
        PORT
      }
    }
  ]
};