from setuptools import setup

package_name = 'camera_tracking'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='batman',
    maintainer_email='batman@todo.todo',
    description='Camera tracking package',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'camera_follower = camera_tracking.camera_follower:main',
        ],
    },
)
