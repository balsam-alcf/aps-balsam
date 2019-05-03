import os
import shutil
from balsam.core.models import ApplicationDefinition as App

def validate_exe(path):
    '''Ensure the first arg of path is a real executable'''
    exe = shlex.split(path)[0]
    if not shutil.which(exe):
        raise RuntimeError(
            f"{exe} is not a valid executable file. " 
            f"Double-check the path, executable permission, your search PATH "
            f"and ensure the right modules are loaded!"
        )

def validate_paths(app):
    '''Validate app.executable and any attached scripts'''
    optional_fields = [app.preprocess, app.postprocess]
    if hasattr(app, 'envscript'): optional_fields.append(app.envscript)

    validate_exe(app.executable)
    for field in option_fields:
        if field: validate_exe(field)

def from_spec(app_name, app_fields, exe_dir):
    '''Generate App from name and app_fields dict'''
    app = App(name=app_name)

    if 'executable' in app_fields:
        app.executable = app_fields['executable']
    else:
        assert os.path.isdir(exe_dir), f'exe_dir "{exe_dir}" is not a directory!'
        app.executable = os.path.abspath(os.path.join(exe_dir, app.name))

    fixed_args = app_fields.get('fixed_args', [])
    if isinstance(fixed_args, (list, tuple)):
        fixed_args= ' ' + ' '.join(map(str, fixed_args))
    else:
        assert isinstance(fixed_args, str)
        fixed_args = ' ' + fixed_args
    app.executable += fixed_args

    app.preprocess = fixed_args.get('preprocess', '')
    app.postprocess = fixed_args.get('postprocess', '')
    app.envscript = fixed_args.get('envscript', '')
    return app

def define_apps(apps, exe_dir=''):
    '''Populate Apps in DB given build dir and application specs

    Args:
      apps -- dict of application-definitions
            key: application name
            value: application spec (dict)
                fixed_args:             list of arguments that *do not* vary from run-to-run
                executable (optional):  absolute path to executable
                                          if omitted, the executable is {exe_dir}/{application name}
                preprocess (optional):  path to preprocess script
                postprocess (optional): path to postprocess script
                envscript (optional):   path to shell script exporting variables; loading modules
      exe_dir (str, optional) : build directory containing the application binaries
      
    '''
    AppDefs = []
    for app_name, app_fields in apps.items():
        app = from_spec(app_name, app_fields, exe_dir)
        AppDefs.append(app)

    for app in AppDefs:
        validate_paths(app)
        print(f"{app.name} path check: OK")
        if not App.objects.filter(name=app.name).exists():
            app.save()
            print(f"Created app {app.name} in DB")
        else:
            existing_app = App.objects.get(name=app.name)
            existing_app.executable = app.executable
            existing_app.postprocess = app.postprocess
            existing_app.preprocess = app.preprocess
            if hasattr(app, "envscript"):
                existing_app.envscript = app.envscript
            existing_app.save()
            print(f"Updated App {app.name} in DB")
