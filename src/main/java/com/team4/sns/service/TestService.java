package com.team4.sns.service;

import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

public interface TestService {

    String test();
    void uploadImageTest(List<MultipartFile> imageFileList) throws IOException;
}
