# for floor
import math

# for performance measurements
import datetime

# for file listing
import glob

# for copy/move
import shutil

# for RIFE
from rife_ncnn_vulkan_python import Rife

# for opening and saving images
from PIL import Image

# for cpu count
import multiprocessing


# TODO proper doc strings lol
# TODO allow in memory workspacing

class SimpleRifeInserter:
    '''A wrapper class to simplify some scenarios with Rife'''
    # global var for temp filenames
    leading_zeros = 12

    # print performance data to console
    verbose_mode = False

    def __init__(self,
                 gpuid: int = 0,
                 model: str = "rife-v2.3",
                 #model: str = "rife-v4",
                 scale: int = 2,
                 tta_mode: bool = False,
                 uhd_mode: bool = True,
                 num_threads: int = multiprocessing.cpu_count()):

        self.rife = Rife(gpuid, model, scale, tta_mode, uhd_mode, num_threads)

    def set_verbose(self, verbose: bool = True):
        '''
        sets whether to print data (elapsed time for interpolation, copied files ... etc.) during excution.
        '''
        self.verbose_mode = verbose

    def __prefix_suffix_remove(file_name: str, prefix: str, suffix: str):
        '''
        Just a tiny helper to remove suffix and prefix from a string
        '''
        return int(file_name.removeprefix(prefix).removesuffix(suffix))

    def __prefix_suffix_add(self, number: int, prefix: str, suffix: str):
        '''
        Just a tiny helper to add suffix and prefix to a string
        '''
        return prefix + str(number).zfill(self.leading_zeros) + suffix

    def interpolate_image_single_in_memory(self, image0: Image, image1: Image) -> Image:
        if self.verbose_mode:
            a = datetime.datetime.now()

        step = float = 0.5  # != 0.5 creates weird images
        interpolated_image = self.rife.process(image0, image1, step)

        if self.verbose_mode:
            b = datetime.datetime.now()
            print(
                "processing done | step = " + str(step) + " | time[microsecs] = " + str((b-a).microseconds))

        return interpolated_image

    def interpolate_image_single(self, path_in0: str, path_in1: str, path_out: str) -> None:
        '''
        this function creates are interpolated image from 2 images.
        these images should not be far apart (i.e. similar).
        '''
        with Image.open(path_in0) as image0:
            with Image.open(path_in1) as image1:
                # create new image
                interpolated_image = self.interpolate_image_single_in_memory(
                    image0, image1)

                if self.verbose_mode:
                    a = datetime.datetime.now()

                # write the image
                interpolated_image.save(path_out)

                if self.verbose_mode:
                    b = datetime.datetime.now()
                    print(
                        "writing done | time[microsecs] = " + str((b-a).microseconds))

    def __interpolate_image_multiple_recusive(self, b_index: int, e_index: int, file_prefix: str, file_suffix: str):
        '''
        this function will start a recursion to create/interpolate all images between b_index and e_index.
        DOES NOT CREATE/COPY IN/INTO WORKSPACE.
        '''
        # block silly input
        if b_index == e_index:
            # TODO stupid python and it's silly exception types
            raise NameError("indeces must not be equal")

        # this is the index of the image which we will create
        current_index = math.floor(b_index + (e_index - b_index) / 2)

        # we have reached the end of the needed recursion
        if b_index == current_index:
            return

        if self.verbose_mode:
            print("processing image : " + str(current_index) +
                  "| from lower/upper = " + str(b_index) + " and " + str(e_index))

        # filenames for input and interpolated images

        left = self.__prefix_suffix_add(
            b_index, file_prefix, file_suffix)
        right = self.__prefix_suffix_add(
            e_index, file_prefix, file_suffix)
        out = self.__prefix_suffix_add(
            current_index, file_prefix, file_suffix)

        # interpolate the image
        self.interpolate_image_single(left, right, out)

        # recursion to fill the remaining (section of) video
        self.__interpolate_image_multiple_recusive(
            b_index, current_index, file_prefix, file_suffix)
        self.__interpolate_image_multiple_recusive(
            current_index, e_index, file_prefix, file_suffix)

    def __interpolate_image_multiple_stepping(self, b_index: int, e_index: int, file_prefix: str, file_suffix: str):
        '''
        this function will start a recursion to create/interpolate all images between b_index and e_index.
        DOES NOT CREATE/COPY IN/INTO WORKSPACE.
        '''
        # TODO sadly stepping creates weird images

        # block silly input
        if b_index == e_index:
            # TODO stupid python and it's silly exception types
            raise NameError("indices must not be equal")

        # this is number of images (including base images)
        num_images = math.floor(e_index - b_index)
        stepping = 1.0 / num_images

        left = self.__prefix_suffix_add(
            b_index, file_prefix, file_suffix)
        right = self.__prefix_suffix_add(
            e_index, file_prefix, file_suffix)

        # load images
        with Image.open(left) as image0:
            with Image.open(right) as image1:
                # iterate all sets
                for index in range(1, num_images, 1):
                    # generate path
                    out_path = self.__prefix_suffix_add(
                        index + b_index, file_prefix, file_suffix)

                    if self.verbose_mode:
                        print("processing image : " +
                              str(index) + " | " + out_path)

                    # interpolate
                    step = index * stepping
                    out_image = self.interpolate_image_singleEx(
                        image0, image1, step)

                    # save
                    out_image.save(out_path)

    def interpolate_image_multiple(self, begin: str, end: str, working_folder: str):
        '''
        this function will start a recursion to create/interpolate all images between 2 images.    
        '''
        # determine filetype
        split_string = begin[0].split('.')
        file_type = '.' + split_string[len(split_string) - 1]

        # copy to workspace
        shutil.copyfile(begin[0], self.__prefix_suffix_add(
            begin[1], working_folder, file_type))

        shutil.copyfile(end[0], self.__prefix_suffix_add(
            end[1], working_folder, file_type))

        # interpolate using files in workspace
        self.__interpolate_image_multiple_recusive(
            begin[1], end[1], working_folder, file_type)

    def increase_fps(self, file_prefix: str, file_suffix: str, increase_factor: int, working_folder: str):
        '''
        this function will increase the of fps of a video by inflating the number of frames
        with interpolated frames (using rife).
        (Video must converted to a set of files first (i.e. 0.jpg to X.jpg))
        '''
        # get filenames
        pattern = file_prefix + "*" + file_suffix
        raw_input_files = glob.glob(pattern)
        new_input_files = []

        if self.verbose_mode:
            print("manipulating the following images:\n" +
                  '\n'.join(raw_input_files))

        # copy the files with new "inflated" index
        for input_file in raw_input_files:
            # number of file
            as_number = SimpleRifeInserter.__prefix_suffix_remove(
                input_file, file_prefix, file_suffix)

            # get the new number (i.e. index of the image) after "inflation"
            new_number = as_number * increase_factor

            # new filename in working folder
            new_input_file = self.__prefix_suffix_add(
                new_number, working_folder, file_suffix)

            shutil.copyfile(input_file, new_input_file)
            new_input_files.append(new_input_file)

        # iterate through our list and interpolate images
        for in_image in zip(new_input_files, new_input_files[1:]):
            # i.e. the 'i' th image
            left_as_number = SimpleRifeInserter.__prefix_suffix_remove(
                in_image[0], working_folder, file_suffix)

            # i.e. the 'i+1' th image
            right_as_number = SimpleRifeInserter.__prefix_suffix_remove(
                in_image[1], working_folder, file_suffix)

            # start the recursion
            self.__interpolate_image_multiple_recusive(b_index=left_as_number, e_index=right_as_number,
                                                       file_prefix=working_folder, file_suffix=file_suffix)
