const path = require('path')

module.exports = {
    node: 'development',
    entry: './src/components/pages/auth/Firebase.jsx',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js'
    },
    watch: true
}