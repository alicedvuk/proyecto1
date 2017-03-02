var gulp = require('gulp'),
    uglify = require('gulp-uglify'),
    minifyCss = require('gulp-minify-css'),
    sass = require('gulp-sass'),
    rename = require('gulp-rename'),
    plumber = require('gulp-plumber'),
    util = require('gulp-util'),
    sourcemaps = require('gulp-sourcemaps'),
    browserSync = require('browser-sync').create();

var onError = function (error) {
    util.beep();
    util.log(util.colors.red(error));
    this.emit('end');
};

gulp.task('styles', function () {
    gulp.src('src/scss/*.scss')
        .pipe(plumber({errorHandler: onError}))
        .pipe(sourcemaps.init())
            .pipe(sass({errLogToConsole: true}).on('error', sass.logError))
        .pipe(sourcemaps.write({sourceRoot: '.'}))
        .pipe(gulp.dest('css'))
        .pipe(minifyCss())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('css'))
});

gulp.task('scripts', function () {
    gulp.src('src/js/**/*.js')
        .pipe(plumber({errorHandler: onError}))
        .pipe(gulp.dest('js'))
        .pipe(uglify())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('js'))
});

gulp.task('serve', function () {
    browserSync.init({
        proxy: "localhost:8000",
        host: "0.0.0.0",
        port: "8001",
        open: false,
        notify: false
    });
});

gulp.task('watch', function () {
    gulp.watch('css/**/*').on('change', function (file) {
        browserSync.reload(file.path);
    });

    gulp.watch('src/js/**/*.js', ['scripts'], browserSync.reload);
    gulp.watch('src/scss/**/*.scss', ['styles']);

    gulp.watch('../templates/**/*.html').on('change', browserSync.reload);
});

gulp.task('build', ['styles', 'scripts']);
gulp.task('default', ['build', 'watch', 'serve']);
