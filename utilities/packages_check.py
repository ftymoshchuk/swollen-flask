import pkg_resources


#  Checks if packages in requirements.txt are match with local env
def read_requirements(file):
    with open(file, 'r') as f:
        return f.readlines()

def parse_requirements(lines):
    requirements = {}
    for line in lines:
        if '==' in line:
            pkg, version = line.strip().split('==')
            requirements[pkg] = version
    return requirements

def get_local_versions():
    local_packages = {}
    for dist in pkg_resources.working_set:
        local_packages[dist.project_name] = dist.version
    return local_packages

def compare_versions(req, local):
    diff = {}
    for pkg in req:
        if pkg in local:
            if req[pkg] != local[pkg]:
                diff[pkg] = (req[pkg], local[pkg])
        else:
            diff[pkg] = (req[pkg], 'not installed')
    return diff

req = parse_requirements(read_requirements('requirements.txt'))
local = get_local_versions()

differences = compare_versions(req, local)

if differences:
    print("Differences found:")
    for pkg, versions in differences.items():
        print(f"{pkg}: {versions[0]} -> {versions[1]}")
else:
    print("No differences found.")
