# Offline build fails: a dependency can't be found

`python -m builder build` assembles the install tree for our service under `/app/out` from the
packages in `/app/build.json`. Read `/app/docs/build.md` first.

The build is currently broken: it stops with

    package not found in any index: telemetry-sdk

`telemetry-sdk` is a dependency of `reportlib`, which our `app` needs. It is not in the public
`/app/wheelhouse`, so the resolver can't find it and the build never produces `/app/out`.

Please make `python -m builder build` complete, so `/app/out/site-packages/` contains `app` and
everything it depends on, and the command exits 0. It should work for any build of this shape,
driven from `build.json`.

Keep the rest working, including the shipped suite: `python -m pytest /app/tests`.
