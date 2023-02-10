module.exports = function (grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            files: ['src/styles/*.scss', 'src/svg/*.svg'],
            tasks: ['sass', 'copy']
        },
        sass: {
            dist: {
                files: {
                    'src/static/css/site.css': ['src/styles/site.scss', 'bower_components/dist/css/**/*.css']
                }
            }
        },
        copy: {
            files: {
                expand: true,
                flatten: true,
                src: ['src/svg/*.svg'],
                dest: 'src/static/img',
                filter: 'isFile'
            }

        }
    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-copy');

    grunt.registerTask('default', ['sass', 'copy']);

};