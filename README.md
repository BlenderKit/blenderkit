# Blenderkit add-on

BlenderKit add-on is the official add-on of the [BlenderKit](https://www.blenderkit.com/) service for Blender 3D.
It enables users to upload, search, download, and rate different assets for Blender 3D.
It works together with BlenderKit online database of models.

## Development

### Building the add-on

Use `dev.py` script to build the add-on.
This script will copy relevant files to `out/blenderkit` directory (ignoring all files which are not needed in the add-on).
From this source the script will then create a zip file at `out/blenderkit.zip`.
This zip then can be used as a release of BlenderKit.

To build run:
```
python dev.py build
```

#### Development build: build and copy to Blender for quick testing

Script `dev.py` provides handy option `--install-at` to copy the `out/blenderkit` directly to Blender so you can quickly test the build just by starting the Blender without any further steps.
Just specify path to addons directory in `--install-at` flag.
Script will then remove old `blenderkit` directory in addons location and replace it with current build.

To build and copy to Blender 3.2.x addons directory run:

```
python dev.py build --install-at /path/to/blender/3.2/scripts/addons
```

### Making a release

To release do:
1. make sure code is OK: version is set, dependencies are updated in master branch
2. wait for automated build on master branch to be finished
3. download the ZIP
4. rename to `blenderkit-x.y.z`
5. upload to Github

Alternatively if automated builds are broken, build locally:
1. make sure code is OK: version is set, dependencies are updated
2. run `python dev.py build` to build the zip file in `out/blenderkit.zip`
3. double check the zip is OK
4. that's all, upload to Github!

## Testing

BlenderKit add-on uses tests implemented through `unittest` module.
As the add-on and its submodules require `bpy` module and interaction with Blender, the tests needs to be executed in the Python inside of the Blender.
This makes the tests to be on the edge between unit tests and integration tests.

The tests are defined in files `test_<name-of-tested-file>.py` and their starting point is in file `test.py` which is executed from `dev.py` script.

### Local testing

To test the add-on locally, make sure you have a Blender on your PATH.
Then run:

```
python dev.py test --install-at /path/to/blender/3.2/scripts/addons
```

NOTE: please make sure that version in the `--install-at` path must match the version of the Blender version you have on your PATH.
Otherwise the add-on with test files will be copied to Blender version 3.x, but tests will run on different Blender version 3.a with outdated BlenderKit build.

### Automated testing: CI/CD

We run automated tests on: Pull Requests.
The tests and checks which must pass for PR to be accepted are:
- unit/integration tests on several versions of Blender 3.x.,
- `isort` check,
- automated build of the add-on.

Those CI/CD jobs are realized through Github workflows and are defined in `.github/workflows` directory.
For Pull Requests jobs it is in file: `.github/workflows/PR.yml`.
