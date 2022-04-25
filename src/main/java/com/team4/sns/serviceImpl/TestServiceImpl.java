package com.team4.sns.serviceImpl;

import com.team4.sns.mapper.TestMapper;
import com.team4.sns.service.TestService;
import com.team4.sns.util.S3Util;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@Service
@RequiredArgsConstructor
public class TestServiceImpl implements TestService {

    private final TestMapper testMapper;
    private final S3Util s3Util;

    @Override
    public String test() {
        return testMapper.test();
    }

    @Override
    public void uploadImageTest(List<MultipartFile> imageFileList) throws IOException {
        s3Util.uploadObject(imageFileList);
    }
}
