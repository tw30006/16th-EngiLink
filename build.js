const esbuild = require('esbuild');

esbuild.build({
    entryPoints: ["static/js/entry.js"],
    bundle: true,
    outfile: "static/js/bundle.js",
}).catch(() => process.exit(1));
