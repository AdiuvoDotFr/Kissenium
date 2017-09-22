var gulp = require('gulp');
var minify = require('gulp-minify');
var concat = require('gulp-concat');
var cssmin = require('gulp-cssmin');
var rename = require('gulp-rename');

gulp.task('minify', function() {
  gulp.start('minify-js');
  gulp.start('minify-css');
});

gulp.task('concat', function() {
  gulp.start('concat-js');
  gulp.start('concat-css');
});

gulp.task('minify-js', function() {
    gulp.src('js/*.js')
        .pipe(minify({
            ext:{
                min:'.min.js'
            },
            exclude: ['tasks'],
            ignoreFiles: ['*.min.js']
        }))
        .pipe(gulp.dest('js'))
});

gulp.task('concat-js', function() {
  return gulp.src(['./js/jquery-3.2.1.min.js', './js/jquery.xpath.min.js', './js/jquery.dim-background.min.js', './js/spop.min.js'])
    .pipe(concat('kissenium.min.js'))
    .pipe(gulp.dest('./dist/'));
});

gulp.task('minify-css', function () {
    gulp.src('css/*.css')
        .pipe(cssmin())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('css'));
});

gulp.task('concat-css', function() {
  return gulp.src('./css/*.min.css')
    .pipe(concat('kissenium.min.css'))
    .pipe(gulp.dest('./dist/'));
});